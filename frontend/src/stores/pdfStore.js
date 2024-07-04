import { defineStore } from 'pinia'

export const usePdfStore = defineStore({
  id: 'pdf',
  state: () => ({
    pdfData: {
      text: [],
      images: []
    }
  }),
  actions: {
    setPdfData(data) {
      this.pdfData = data
    }
  }
})
