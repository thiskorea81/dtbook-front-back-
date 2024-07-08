<template>
    <div>
      <h2>PDF 업로드 및 변환</h2>
      <input type="file" @change="handleFileUpload" />
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router'
  import { usePdfStore } from '@/stores/pdfStore'
  import axios from 'axios'
  
  export default {
    setup() {
      const pdfStore = usePdfStore()
      const router = useRouter()
  
      const handleFileUpload = async (event) => {
        const file = event.target.files[0]
        const formData = new FormData()
        formData.append('file', file)
  
        try {
          console.log('Uploading file:', file)
          const response = await axios.post('api/extract', formData, {
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
  
  <style scoped>
  input[type="file"] {
    margin-bottom: 20px;
  }
  </style>
  