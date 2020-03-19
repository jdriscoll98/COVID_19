import axios from 'axios'
import router from '../../router'

const state = {
  verify_user: '',
  error: ''
}

const getters = {
  error: state => state.error
}

const mutations = {
  verifySubscriber: (state, { telephone }) => {
    state.verify_user = telephone
    state.error = ''
    router.push('/verify')
  },
  invalidCode: (state, error) => {
    state.error = error.response.data.error
  },
  updateError: (state, { telephone, location }) => {
    if (telephone) {
      state.error = telephone[0]
    } else {
      state.error = location[0]
    }
  }

}

const actions = {
  async resendCode () {
    const telephone = state.verify_user
    await axios.post('api/subscribers/resend', {
      telephone
    })
      .catch(e => {
      // pass
      }
      )
  },
  async beginFlow ({ commit }, telephone) {
    const number = telephone.telephone
    console.log(number)
    await axios.post('api/subscribers/begin_flow', {
      number
    })
  },
  async addSubscriber ({ commit }, { telephone, location }) {
    await axios.post('api/subscribers', {
      telephone,
      location
    })
      .then(response => {
        commit('verifySubscriber', response.data)
      })
      .catch(error => {
        commit('updateError', error.response.data)
      })
  },
  async verifyCode ({ commit }, key) {
    const telephone = state.verify_user

    await axios.post('api/subscribers/verify', {
      key,
      telephone
    })
      .then((response) => {
        router.push('/thankyou')
        this.dispatch('beginFlow', {
          telephone
        })
      })
      .catch(error => {
        commit('invalidCode', error)
      })
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
