<template>
  <div>
    <button @click="goHome">홈</button>
    <div v-if="pdfData.text.length > 0">
      <button @click="prevPage" :disabled="currentPage === 0">이전 페이지</button>
      <button @click="nextPage" :disabled="currentPage === pdfData.text.length - 1">다음 페이지</button>
      <div class="pdf-page">
        <div class="pdf-image">
          <div v-for="image in getImageFilenamesForPage(currentPage + 1)" :key="image">
            <img :src="`http://localhost:8000/images/${image}`" alt="PDF 이미지" />
          </div>
        </div>
        <div class="pdf-text">
          <p>{{ pdfData.text[currentPage] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { usePdfStore } from '@/stores/pdfStore'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const pdfStore = usePdfStore()
    const pdfData = pdfStore.pdfData
    const router = useRouter()
    const currentPage = ref(0)

    const getImageFilenamesForPage = (pageNum) => {
      return pdfData.images.filter(image => image.includes(`page${pageNum}_`))
    }

    const nextPage = () => {
      if (currentPage.value < pdfData.text.length - 1) {
        currentPage.value += 1
      }
    }

    const prevPage = () => {
      if (currentPage.value > 0) {
        currentPage.value -= 1
      }
    }

    const goHome = () => {
      router.push('/')
    }

    console.log('PDF Data in Result:', pdfData)

    return { pdfData, currentPage, nextPage, prevPage, goHome, getImageFilenamesForPage }
  }
}
</script>

<style>
.pdf-page {
  display: flex;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  align-items: center;
  justify-content: center;
}

.pdf-image {
  flex: 1;
  text-align: center;
}

.pdf-image img {
  max-width: 100%;
  height: auto;
}

.pdf-text {
  flex: 1;
  text-align: left;
  white-space: pre-wrap; /* Preserve whitespace and line breaks */
  padding-left: 20px;
}

button {
  margin: 10px;
}
</style>
