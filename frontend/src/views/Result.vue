// frontend/src/views/Result.vue
<template>
  <header>
    <h2>PDF Page</h2>
    <div v-if="pdfData.text.length > 0">
      <button @click="goHome">업로드 화면</button>
      <button @click="prevPage" :disabled="currentPage === 0">이전 페이지</button>
      <button><span>{{ currentPage + 1 }}</span>p</button>
      <button @click="nextPage" :disabled="currentPage === pdfData.text.length - 1">다음 페이지</button>
    </div>
  </header>
  <section>
    <article>
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
    </article>
    <aside>
      <Chat />
    </aside>
  </section>
  <footer>
    <div v-if="pdfData.text.length > 0">
      <button @click="prevPage" :disabled="currentPage === 0">이전 페이지</button>
      | <span>{{ currentPage + 1 }}</span>p |
      <button @click="nextPage" :disabled="currentPage === pdfData.text.length - 1">다음 페이지</button>
    </div>
  </footer>
</template>

<script>
import { ref } from 'vue'
import { usePdfStore } from '@/stores/pdfStore'
import { useRouter } from 'vue-router'
import Chat from './Chat.vue'

export default {
  components: {
    Chat
  },
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

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

header {
  background-color: #4CAF50;
  color: white;
  padding: 1rem 0;
  text-align: center;
  width: 100%;
  max-width: 1280px;
}

h2 {
  margin: 0;
}

section {
  display: flex;
  flex: 1;
  margin: 20px;
  width: 100%;
  max-width: 1280px;
  box-sizing: border-box;
}

article {
  flex: 3;
  padding: 20px;
  background: white;
  margin-right: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

aside {
  flex: 1;
  padding: 20px;
  background: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

aside ul {
  padding: 0;
}

aside li {
  margin: 10px 0;
}

aside a {
  text-decoration: none;
  color: #4CAF50;
}

aside p {
  text-decoration: none;
  color: #4CAF50;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 10px 0;
  margin-top: auto;
  width: 100%;
  max-width: 1280px;
}

footer a {
  color: white;
  text-decoration: none;
  margin: 0 10px;
}

footer a:hover {
  text-decoration: underline;
}
</style>
