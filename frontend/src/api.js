export const myselfApi = {
  weekAnimate: '/api/myself/week-animate/',
  animateInfo: '/api/myself/animate-info/',
  finishList: '/api/myself/finish-list/',
  finishAnimate: '/api/myself/finish-animate/',
  animateEpisodeDone: '/api/myself/animate-episode-done/',
  animateInfoEpisodeInfo: '/api/myself/animate-info/{animateID}/episode-info/'
}

export const myApi = {
  myLog: (page, size) => `/api/my/log/?page=${page}&size=${size}`
}
