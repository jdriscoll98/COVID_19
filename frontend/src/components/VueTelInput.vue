<template>
  <vue-tel-input v-model="value"></vue-tel-input>
</template>
<script>
import { VueTelInput } from 'vue-tel-input'

export default {
  components: {
    VueTelInput
  },
  data () {
    return {
      value: ''
    }
  }
}
</script>
