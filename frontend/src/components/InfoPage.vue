<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card card-block pl-5 pr-5 pt-3 pb-3">
                    <h4 class="text-center title">What am I signing up for?</h4>
                    <div class="list pl-3 pr-3">

                        <ul>
                            <li>A daily text listing the number of cases worldwide, in your country, and your state/province.</li>
                            <li>(Optional) A daily text with  4 of the top news articles concerning COVID-19</li>
                        </ul>
                    </div>
                    <a href="/" class="btn-success text-center py-1">Go Back and Sign Up!</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'InfoPage'
}
</script>

<style scoped>
.card {
  background-color: rgb(245, 245, 245, .9);
  border: 1px solid lime;
  margin-top: 25%;
}

.btn-success {
    border: 1px solid black;
    border-radius: 10px;
}
.title {
    font-weight: 800
}
.subtitle {
    font-weight: 400;
}
</style>
