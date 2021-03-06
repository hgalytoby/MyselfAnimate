export const myselfApi = {
  weekAnimate: '/api/myself/week-animate/',
  animateInfo: (url) => `/api/myself/animate-info/?url=${url}`,
  searchAnimate: (url) => `/api/myself/url-search/?url=${url}`,
  finishList: '/api/myself/finish-list/',
  finishAnimate: '/api/myself/finish-animate/',
  animateEpisodeDone: '/api/myself/animate-episode-done/',
  animateInfoEpisodeInfo: (animateID) => `/api/myself/animate-info/${animateID}/episode-info/`,
  destroyManyAnimate: '/api/myself/destroy-many-animate/'
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
  homeMenu: '/api/anime1/home-menu/',
  season: (season) => `/api/anime1/season/${season}/`,
  destroyManyAnimate: '/api/anime1/destroy-many-animate/'
}
