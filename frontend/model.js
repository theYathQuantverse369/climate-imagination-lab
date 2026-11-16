/* Browser fallback for demos opened without the Python server. Keep these
   transparent classroom rules aligned with backend/server.py. */
(function (root) {
  const cityProfiles = {
    Chennai: {state:"Tamil Nadu",coastal:.88,heat:.82,rain:.76,urban:.73,eco:.58,lat:13.08,lon:80.27},
    Mumbai: {state:"Maharashtra",coastal:.94,heat:.69,rain:.88,urban:.86,eco:.55,lat:19.08,lon:72.88},
    Kolkata: {state:"West Bengal",coastal:.76,heat:.79,rain:.82,urban:.82,eco:.62,lat:22.57,lon:88.36},
    Delhi: {state:"Delhi",coastal:.04,heat:.94,rain:.55,urban:.88,eco:.68,lat:28.61,lon:77.21},
    Bengaluru: {state:"Karnataka",coastal:.05,heat:.61,rain:.65,urban:.72,eco:.50,lat:12.97,lon:77.59},
    Kochi: {state:"Kerala",coastal:.90,heat:.65,rain:.91,urban:.61,eco:.46,lat:9.93,lon:76.27},
    Ahmedabad: {state:"Gujarat",coastal:.22,heat:.92,rain:.43,urban:.77,eco:.71,lat:23.02,lon:72.57},
    Hyderabad: {state:"Telangana",coastal:.08,heat:.83,rain:.62,urban:.78,eco:.61,lat:17.39,lon:78.49}
  };
  const horizons={2030:.55,2040:.72,2050:1,2070:1.23,2090:1.45};
  const actions={
    shade:{"Heat stress":15,"Urban vulnerability":3},
    cool_roofs:{"Heat stress":12,"Urban vulnerability":4},
    drainage:{"Flood exposure":17,"Extreme rainfall":10,"Urban vulnerability":8},
    wetlands:{"Flood exposure":13,"Extreme rainfall":6,"Ecological pressure":9},
    permeable:{"Flood exposure":10,"Extreme rainfall":8,"Ecological pressure":3},
    cooling_centres:{"Heat stress":10,"Urban vulnerability":9},
    early_warning:{"Flood exposure":7,"Extreme rainfall":9,"Urban vulnerability":8},
    transit:{"Heat stress":3,"Urban vulnerability":8,"Ecological pressure":8},
    water_saving:{"Heat stress":4,"Ecological pressure":9}
  };
  function calculate(s) {
    const city=s.city||"Chennai", warming=Number(s.warming), rainfall=Number(s.rainfall), year=Number(s.year), adaptation=s.adaptation||"none";
    const investment=Number(s.investment??65);
    if(!cityProfiles[city])throw Error("Choose one of the listed cities.");
    if(![1,2,3].includes(warming))throw Error("Choose +1°C, +2°C, or +3°C warming.");
    if(![70,85,100,115,130].includes(rainfall))throw Error("Choose one of the rainfall options.");
    if(!Object.hasOwn(horizons,year))throw Error("Choose one of the listed time horizons.");
    if(adaptation!=="none"&&!Object.hasOwn(actions,adaptation))throw Error("Choose one of the listed actions.");
    if(!Number.isInteger(investment)||investment<0||investment>100)throw Error("Investment must be between 0 and 100 percent.");
    const p=cityProfiles[city],h=horizons[year];
    const raw={
      "Heat stress":19+p.heat*37+warming*9*h,
      "Flood exposure":12+p.coastal*31+p.rain*20+(rainfall-100)*.43+warming*3.5*h-investment*.29,
      "Extreme rainfall":14+p.rain*36+(rainfall-100)*.55+warming*4*h,
      "Urban vulnerability":15+p.urban*50+warming*4*h+Math.max(0,rainfall-100)*.11,
      "Ecological pressure":12+p.eco*43+warming*7*h+Math.max(0,rainfall-100)*.1
    };
    for(const [name,amount] of Object.entries(actions[adaptation]||{}))raw[name]-=amount;
    const risks=Object.fromEntries(Object.entries(raw).map(([name,value])=>[name,Math.max(0,Math.min(100,Math.round(value)))]));
    return {city,state:p.state,warming,rainfall,year,adaptation,investment,risks,curve:riskCurve(s),
      profile:{coastal_influence:p.coastal,heat_sensitivity:p.heat,rainfall_sensitivity:p.rain,urban_pressure:p.urban,ecological_sensitivity:p.eco}};
  }
  function riskCurve(s) {
    const p=cityProfiles[s.city||"Chennai"],year=Number(s.year)||2050,h=horizons[year],rainShift=Number(s.rainfall)-100,investment=Number(s.investment??65),extraFlood=(actions[s.adaptation]||{})["Flood exposure"]||0;
    const series={temperature:[],flood_unmitigated:[],people_affected:[],flood_invested:[]};
    for(let i=0;i<=8;i++){
      const warming=i*.5,temp=22+p.heat*27+warming*10.2*h;
      const flood=17+p.coastal*14+p.rain*12+rainShift*.18+warming*8.8*h;
      const people=19+p.urban*17+p.coastal*3+rainShift*.1+warming*8.5*h;
      for(const [key,value] of Object.entries({temperature:temp,flood_unmitigated:flood,people_affected:people,flood_invested:flood-investment*.29-extraFlood}))series[key].push({warming,risk:Math.max(0,Math.min(100,Math.round(value)))});
    }
    return series;
  }
  const api={cities:Object.entries(cityProfiles).map(([name,p])=>({name,state:p.state,lat:p.lat,lon:p.lon})),calculate,riskCurve};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  if(root)root.ClimateScenarioModel=api;
})(typeof window!=="undefined"?window:null);

