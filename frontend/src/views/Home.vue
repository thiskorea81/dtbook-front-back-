<template>
  <div>
    <h1>PDF 업로드</h1>
    <input type="file" @change="handleFileUpload" />
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter } from 'vue-router'
import { usePdfStore } from '@/stores/pdfStore'

export default {
  setup() {
    const pdfStore = usePdfStore()
    const router = useRouter()

    const handleFileUpload = async (event) => {
      const file = event.target.files[0]
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post('http://localhost:8000/extract', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        const pdfData = response.data
        console.log('Extracted PDF Data:', pdfData)
        pdfStore.setPdfData(pdfData)
        router.push('/result')
      } catch (error) {
        console.error('Error uploading file:', error)
      }
    }

    return { handleFileUpload }
  }
}
</script>
