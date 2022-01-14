export const myselfApi = {
  weekAnimate: '/api/myself/week-animate/',
  // animateInfo: (url) => `/api/myself/animate-info/?url=${url}`,
  animateInfo: '/api/myself/animate-info/',
  searchAnimate: '/api/myself/url-search/',
  finishList: '/api/myself/finish-list/',
  finishAnimate: '/api/myself/finish-animate/',
  animateEpisodeDone: '/api/myself/animate-episode-done/',
  animateInfoEpisodeInfo: (animateID) => `/api/myself/animate-info/${animateID}/episode-info/`
}

export const myApi = {
  log: '/api/my/log/',
  settings: '/api/my/settings/',
  system: (page, size) => `/api/my/log/system/?page=${page}&size=${size}`,
  history: (page, size) => `/api/my/log/history/?page=${page}&size=${size}`
}

export const anima1Api = {
  animateList: '/api/anime1/animate-list/',
  animateInfo: (url) => `/api/anime1/animate-info/?url=${url}`,
  animateEpisodeDone: '/api/anime1/animate-episode-done/',
  homeMenu: 'api/anime1/home-menu/'
}
