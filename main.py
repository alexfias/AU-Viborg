# --------- 1) Scenarios  ----------
# 1: 840 kWp PV, no battery
# 2: +0.72 MWh battery
# 3: 2.0 MW PV + 2.5 MWh battery
# 4: 3.9 MW PV + 8.9 MWh battery
# 5: 1.3 MW PV + 1.3 MW wind + 4.9 MWh battery
SC = 1
pars = {
  1: dict(pv_kw=840,  batt_mwh=0.0, wind_kw=0),
  2: dict(pv_kw=840,  batt_mwh=0.72, wind_kw=0),
  3: dict(pv_kw=2000, batt_mwh=2.5,  wind_kw=0),
  4: dict(pv_kw=3900, batt_mwh=8.9,  wind_kw=0),
  5: dict(pv_kw=1300, batt_mwh=4.9,  wind_kw=1300),
}[SC]


# --------- 2) Network ----------
n = pypsa.Network()
n.set_snapshots(snapshots)
n.add("Bus","elec"); n.add("Bus","heat"); n.add("Bus","gas")

n.add("Load","L_e", bus="elec", p_set=el/1e3)      # kW
n.add("Load","L_h", bus="heat", p_set=heat/1e3)

# CHP: gas -> electricity (40%) + heat (50%), fixed 635 kWel
n.add("Link","CHP",
      bus0="gas", bus1="elec", bus2="heat",
      p_nom=635, efficiency=0.40, efficiency2=0.50, marginal_cost=0)

# Biogas supply price (€/kWh -> €/MWh)
n.add("Carrier","biogas")
n.add("Generator","biogas_supply", bus="gas", carrier="biogas",
      p_nom=1e6, marginal_cost=0.17*1000)
