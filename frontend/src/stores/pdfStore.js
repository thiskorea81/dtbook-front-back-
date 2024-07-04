
//dtbooks\src\stores\pdfStore.js
import { defineStore } from 'pinia'

export const usePdfStore = defineStore('pdf', {
  state: () => ({
    pdfData: null
  }),
  actions: {
    setPdfData(data) {
      this.pdfData = data
    }
  }
})
