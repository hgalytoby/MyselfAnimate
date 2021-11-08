import { Fancybox } from '@fancyapps/ui/src/Fancybox'

export const useStartFancy = (video) => {
  Fancybox.show([
    {
      src: video,
      type: 'iframe',
      preload: false
    }], {}) // starts fancybox with the gallery object
}
