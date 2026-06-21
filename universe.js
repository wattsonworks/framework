/* LIQUIDEX FRAMEWORK — the instrument universe under profile (the "stash").
   The deep-tuned book is a published cross-section; this is the full breadth available on request. */
window.UNIVERSE = {
  total: 205, tuned: 107, classes: 5,
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
    { key: 'crypto',  label: 'Digital assets',       syms: ['BTC','ETH','SOL','BNB','XRP','ADA','AVAX','LINK','DOGE','DOT','LTC','BCH','ATOM','NEAR','INJ','FIL','RENDER','FET','ARB','OP','APT','SUI','UNI','AAVE','TRX','ICP','POL','PEPE','ENA','TIA','SEI','JUP','LDO','RUNE','WIF','ONDO','MKR'] },
    { key: 'fx',      label: 'FX majors',            syms: ['EURUSD','GBPUSD','USDJPY','USDCHF','AUDJPY','NZDUSD','USDCAD','AUDUSD','GBPJPY','EURJPY','EURGBP'] },
    { key: 'comspot', label: 'Commodities (spot)',   syms: ['XAUUSD','XAGUSD','XCUUSD','WTICOUSD','NATGASUSD'] },
    { key: 'index',   label: 'Global indices',       syms: ['SPX500USD','NAS100USD','US30USD','DE30EUR','UK100GBP'] }
  ],
  // instruments with a published, deep-tuned recipe (the rest are profiled and available on request)
  tunedSet: ["AAVE", "ADA", "ADI", "AMAT", "AMD", "APT", "ARB", "ARM", "ASML", "ATOM", "AUDJPY", "AUDUSD", "AVAX", "AVGO", "BCH", "BNB", "BTC", "COST", "DE", "DE30EUR", "DIA", "DOGE", "DOT", "ENA", "ETH", "ETH-CB", "ETN", "EURGBP", "EURJPY", "EURUSD", "FET", "FIL", "GBPJPY", "GBPUSD", "GLD", "ICP", "IGV", "INJ", "INTC", "IWM", "JPM", "JUP", "KLAC", "KO", "LDO", "LINK", "LRCX", "LTC", "MA", "MCHP", "MPWR", "MRVL", "MU", "NAS100USD", "NATGASUSD", "NEAR", "NVDA", "NXPI", "NZDUSD", "ON", "ONDO", "OP", "ORCL", "PANW", "PEP", "PEPE", "QCOM", "QQQ", "RENDER", "RUNE", "SCHD", "SEI", "SMH", "SOL", "SOXX", "SPX500USD", "SPY", "SUI", "TIA", "TLT", "TRX", "TSEM", "TSM", "TXN", "UK100GBP", "UNI", "US30USD", "USDCAD", "USDCHF", "USDJPY", "V", "VGT", "VOO", "WIF", "WTICOUSD", "XAGUSD", "XAUUSD", "XCUUSD", "XLE", "XLF", "XLI", "XLK", "XLP", "XLV", "XLY", "XOM", "XRP"]
};
