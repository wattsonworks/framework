/* LIQUIDEX FRAMEWORK — the instrument universe under profile (the "stash").
   The deep-tuned book is a published cross-section; this is the full breadth available on request. */
window.UNIVERSE = {
  total: 144, tuned: 53, classes: 3,
  sectors: [
    { key: 'fin',     label: 'Financials',          syms: ['JPM','BAC','C','GS','MS','SCHW','PNC','USB','BK','COF','V','MA','SPGI','ICE','CME'] },
    { key: 'soft',    label: 'Software / SaaS',      syms: ['CRM','ORCL','NOW','PANW','FTNT','MDB','DDOG','HUBS','TEAM','SHOP','INTU','ADBE','APP','NET','ZS','SNOW'] },
    { key: 'cloud',   label: 'Cloud / AI-infra',     syms: ['ANET','VRT','DELL','HPE','SMCI','CSCO','IBM','DLR','EQIX'] },
    { key: 'hc',      label: 'Healthcare',           syms: ['UNH','ABBV','JNJ','ABT','MDT','SYK','TMO','DHR','AMGN','BMY','GILD','REGN','VRTX'] },
    { key: 'ind',     label: 'Industrials',          syms: ['DE','ETN','PH','EMR','CARR','TT','HON','RTX','LMT','NOC','BA','WM'] },
    { key: 'cons',    label: 'Consumer',             syms: ['COST','PG','KO','PEP','MCD','SBUX','LOW','HD','TJX','CMG','NKE'] },
    { key: 'energy',  label: 'Energy',               syms: ['XOM','CVX','COP','EOG','SLB','OXY','MPC','VLO','PSX'] },
    { key: 'telecom', label: 'Telecom / Media',      syms: ['CHTR','CMCSA','T','VZ','TMUS','DIS'] },
    { key: 'auto',    label: 'Auto',                 syms: ['GM','F','RACE','RIVN','LCID'] },
    { key: 'semis',   label: 'Semiconductors',       syms: ['KLAC','NXPI','QCOM','TXN','MCHP','MPWR','ADI','ON','AVGO','NVDA','AMD','MRVL','ARM','LRCX','AMAT','ASML','TSM','INTC','TSEM','MU'] },
    { key: 'etf',     label: 'Index & Sector ETFs',  syms: ['DIA','IWM','SMH','XLF','XLK','XLI','XLE','XLV','XLP','XLY','VGT','VOO','SCHD','IGV','SOXX','SPY','QQQ','GLD','TLT'] },
    { key: 'commod',  label: 'Commodities',          syms: ['SLV','GDX','USO','DBA','CPER'] },
    { key: 'crypto',  label: 'Digital assets',       syms: ['BTC','ETH','SOL'] },
    { key: 'fx',      label: 'FX majors',            syms: ['EURUSD'] }
  ],
  // the 53 instruments with a published, deep-tuned recipe (the rest are profiled and available on request)
  tunedSet: ['JPM','V','MA','ORCL','PANW','DE','ETN','COST','KO','PEP','XOM',
    'KLAC','NXPI','QCOM','TXN','MCHP','MPWR','ADI','ON','AVGO','NVDA','AMD','MRVL','ARM','LRCX','AMAT','ASML','TSM','INTC','TSEM','MU',
    'DIA','IWM','SMH','XLF','XLK','XLI','XLE','XLV','XLP','XLY','VGT','VOO','SCHD','IGV','SOXX','SPY','QQQ','GLD','TLT',
    'BTC','ETH','SOL']
};
