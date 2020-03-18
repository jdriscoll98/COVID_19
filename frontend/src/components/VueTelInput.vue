<template>
  <vue-tel-input v-model="value" v-on:input="changeTelephone"></vue-tel-input>
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
  },
  methods: {
    changeTelephone () {
      this.$emit('change-tel', this.value)
    }
  }
}
</script>
