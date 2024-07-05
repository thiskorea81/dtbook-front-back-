// frontend/src/views/Home.vue
<template>
  <header>
    <h2>HOME</h2>
    <button @click="goResult">결과 화면</button>
  </header>
  <section>
    <article>
      <h2>PDF 업로드 및 변환</h2>
      <input type="file" @change="handleFileUpload" />
      <div v-if="pdfData">
        <h2>PDF 내용</h2>
        <div v-for="(text, index) in pdfData.text" :key="index">
          <h3>페이지 {{ index + 1 }}</h3>
          <div v-html="text"></div>
            <div v-for="(image, imgIndex) in pdfData.images" :key="imgIndex">
              <img :src="`http://localhost:8000/images/${image}`" alt="PDF 이미지" />
            </div>
          </div>
        </div>    
    </article>
  </section>
  <footer></footer>
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
        console.log('Uploading file:', file)
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

    const goResult = () => {
      router.push('/result')
    }

    return { handleFileUpload, goResult }
  }
}
</script>

<style>
/* 스타일을 추가하여 UI를 개선합니다 */
h1, h2, h3 {
  font-family: Arial, sans-serif;
  color: #333;
}

input[type="file"] {
  margin-bottom: 20px;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #ddd;
}

p {
  font-size: 16px;
  line-height: 1.5;
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
