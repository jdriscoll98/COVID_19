<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card card-block pl-5 pr-5 pt-3 pb-3">
                    <h3 class="text-center">Please enter the code you received!</h3>
                    <h5 class="error text-center"> {{ error }}</h5>
                    <form @submit="onSubmit">
                        <div class="form-group row ">
                            <div class="col-12">
                            <input  id="single-factor-code-text-field" type="text" class="form-control mb-2" autocomplete="one-time-code" v-model="code" name="code" />
                            </div>
                            <button class="btn btn-success btn-sm col-md-6 offset-md-3 col-10 offset-1" type="submit">Verify</button>
                        </div>
                    </form>
                    <div class="text-center"><button class="btn btn-light bg-transparent" @click="resendCode">Didn't receive a code? Click here to resend</button></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'VerifyPage',
  data () {
    return {
      code: ''
    }
  },
  methods: {
    ...mapActions(['verifyCode', 'resendCode']),
    onSubmit (e) {
      e.preventDefault()
      this.verifyCode(this.code)
    }
  },
  resendCode () {
    this.$set(this.code, '')
    this.resendCode()
  },
  computed: mapGetters(['error'])
}
</script>

<style scoped>
.card {
  background-color: rgb(245, 245, 245, .9);
  border: 1px solid lime;
  margin-top: 25%;
}
.error {
  color: red;
}
.bg-transparent {
  color: blue;
  text-decoration: underline;
  border: none;
}

</style>
