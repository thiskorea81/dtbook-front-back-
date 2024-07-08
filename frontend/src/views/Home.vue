<template>
  <header>
    <h2>HOME</h2>
    <button @click="goResult">PDF 결과 화면</button>
    <button @click="goBookResult">책 생성 결과 화면</button>
  </header>
  <section>
    <PdfUpload />
    <BookGenerator />
  </section>
  <footer></footer>
</template>

<script>
import { useRouter } from 'vue-router'
import PdfUpload from '@/components/PdfUpload.vue'
import BookGenerator from '@/components/BookGenerator.vue'

export default {
  components: {
    PdfUpload,
    BookGenerator
  },
  setup() {
    const router = useRouter()

    const goResult = () => {
      router.push('/result')
    }

    const goBookResult = () => {
      router.push('/book-result')
    }

    return { goResult, goBookResult }
  }
}
</script>

<style src="./Home.css"></style> <!-- 분리된 스타일 파일을 불러옴 -->