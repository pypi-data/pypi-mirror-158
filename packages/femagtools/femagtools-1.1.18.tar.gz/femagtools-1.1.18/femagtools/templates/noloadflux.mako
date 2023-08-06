-- calculate noload flux and airgap flux density
--
-- model:
--    frequency (Hz),
--    current (max A rms),
--    num_currents (number of samples, default 8)
--    num_par_wdgs (number of parallel winding groups, default 1)
--
% if model.get('frequency',0):

get_sreg_keys("srkeys") -- get all valid subregions
for j=1, #srkeys do
  srname = get_sreg_data('name', srkeys[j])
  if srname == 'Bar ' then
    sekeys=get_sreg_data("sekeys",srkeys[j])
    ndkeys=get_spel_data("ndkeys",sekeys[1])
    xm, ym = 0, 0
    for i=1, #ndkeys do
      x, y = get_node_data("xy", ndkeys[i])
      xm = xm + x
      ym = ym + y
    end
    x,y=xm/#ndkeys, ym/#ndkeys
    set_mat_cond(x,y, 0, 100.0 )
  end
end
%endif
ksym = m.num_poles/m.npols_gen
maxit = m.num_nonl_it
du_u0 = m.error_perm
rmod = m.perm_mode
cmod = 0
m.current=math.sqrt(2)*${model.get('max_current', 0)}  -- max current amplitude

psi={}
cur={}
a=${model.get('num_par_wdgs', 1)}   -- parallel branches

f1 = ${model.get('frequency', 0)} -- frequency
if( f1 > 0 ) then
  state_of_problem('mag_dynamic')
end
file_psi = io.open("noloadflux.dat","w")

nCurrs = ${model.get('num_currents', 8)}
bag = {}
psi_re = {}
psi_im = {}
 for i = 1, nCurrs do
     i1 = i*m.current/nCurrs/a
     cur[1] = {i1*math.cos(4*math.pi/3), i1*math.sin(4*math.pi/3)}
     cur[2] = {i1, 0}
     cur[3] = {i1*math.cos(2*math.pi/3), i1*math.sin(2*math.pi/3)}
     for j=1, 3 do
       def_curr_wdg(j,cur[j][1], cur[j][2])
     end
     calc_field_single({maxit=maxit, maxcop=du_u0,
        permode='restore',freq=f1})

     for j=1,3 do
        Psi_re, Psi_im = flux_winding_wk(j)
        psi_re[j] = ksym*Psi_re/a*m.arm_length -- Vs
        psi_im[j] = ksym*Psi_im/a*m.arm_length -- Vs
      end
      post_models("induct(x)","b")    -- Calculate field distribution
      bag[i] = {}
      n = 1
      for j = 1, table.getn(b), 3 do
       bag[i][n] = {b[j],b[j+1],b[j+2]}
       n = n+1
      end

      file_psi:write(string.format("%g %g %g %g %g %g %g\n",
         a*i1/math.sqrt(2),
         psi_re[1],psi_im[1],
         psi_re[2],psi_im[2],
         psi_re[3],psi_im[3]))
end
file_psi:close()

file_bag = io.open("noloadbag.dat","w")
for i=1, n-1 do
  file_bag:write(string.format("%g ",
       bag[1][i][1]))
  for j=1, #bag do
    file_bag:write(string.format("%g ",
       bag[j][i][2]))
  end
  file_bag:write("\n")
end
file_bag:close()
