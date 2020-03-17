<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3 text-center">
                <div class="card card-block p-3">
                    <h3>COVID-19 Outbreak Upates</h3>
                    <h6>Click <a href="/info">here</a> for more info</h6>
                    <div class="col-md-8 col-sm-10 offset-md-2 offset-sm-1 mt-3">
                        <form @submit="onSubmit">
                            <div class="form-row mb-3">
                                <div class="col">
                                    <VueTelInput />
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="col">
                                  <VueGoogleAutoComplete />
                                </div>
                            </div>
                            <button type="submit" value class="btn btn-dark col-10 mt-4 mb-3">Sign up</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import VueGoogleAutoComplete from '@/components/VueGoogleAutocomplete'
import VueTelInput from '@/components/VueTelInput'
import axios from 'axios'

export default {
  components: {
    VueGoogleAutoComplete,
    VueTelInput
  },
  data () {
    return {
      telephone: '',
      location: ''
    }
  },
  methods: {
    onSubmit (e) {
      e.preventDefault()
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/subscribers',
        data: {
          telephone: this.telephone,
          location: this.location
        }
      })
        .then(function (response) {
          const status = JSON.parse(response.data.response.status)

          if (status === '200') {
            self.$router.push('/')
          }
        })
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

.btn-dark {
    border: 1px solid lime;
}
</style>
