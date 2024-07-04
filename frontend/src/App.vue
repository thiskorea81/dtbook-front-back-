<template>
  <nav>
    <RouterLink to="/">Home </RouterLink>
    <RouterLink to="/result"> Result</RouterLink>
  </nav>
  <router-view />
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: 'App'
}
</script>

<style>
/* 전역 스타일을 여기서 정의할 수 있습니다. */
</style>
