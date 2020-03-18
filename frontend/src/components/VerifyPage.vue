<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card card-block pl-5 pr-5 pt-3 pb-3">
                    <h3 class="text-center">Please enter the code you received!</h3>
                    <form @submit="onSubmit">
                        <div class="form-group row ">
                            <div class="col-12">
                            <input type="text" class="form-control mb-2" v-model="code" name="code" />
                            </div>
                            <button class="btn btn-success btn-sm col-md-6 offset-md-3 col-10 offset-1" type="submit">Verify</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'VerifyPage',
  data () {
    return {
      code: ''
    }
  },
  methods: {
    ...mapActions(['verifyCode']),
    onSubmit (e) {
      e.preventDefault()
      this.verifyCode(this.code)
    }
  }
}
</script>

<style scoped>
.card {
  background-color: rgb(245, 245, 245, .9);
  border: 1px solid lime;
  margin-top: 25%;
}

</style>
