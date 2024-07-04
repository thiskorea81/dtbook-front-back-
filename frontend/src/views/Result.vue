<template>
  <div>
    <h1>PDF 내용</h1>
    <div v-for="(page, index) in pdfData.text" :key="index" class="pdf-page">
      <h2>페이지 {{ index + 1 }}</h2>
      <p class="pdf-text">{{ page }}</p>
      <div v-for="image in getImageFilenamesForPage(index + 1)" :key="image" class="pdf-image">
        <img :src="`http://localhost:8000/images/${image}`" alt="PDF 이미지" />
      </div>
    </div>
  </div>
</template>

<script>
import { usePdfStore } from '@/stores/pdfStore'

export default {
  setup() {
    const pdfStore = usePdfStore()
    const pdfData = pdfStore.pdfData

    const getImageFilenamesForPage = (pageNum) => {
      return pdfData.images.filter(image => image.includes(`page${pageNum}_`))
    }

    console.log('PDF Data in Result:', pdfData)

    return { pdfData, getImageFilenamesForPage }
  }
}
</script>

<style>
.pdf-page {
  border: 1px solid #ccc;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
}

.pdf-text {
  white-space: pre-wrap; /* Preserve whitespace and line breaks */
}

.pdf-image img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}
</style>
