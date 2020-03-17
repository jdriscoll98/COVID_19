<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card card-block pl-5 pr-5 pt-3 pb-3">
                    <h3 class="text-center">What am I signing up for?</h3>
                    <div class="list pl-3 pr-3">
                        <h6>Upon signing up, you will be promted through text to choose from the options below</h6>
                        <ul>
                            <li>A daily text listing the number of cases worldwide, around your area, and in your city</li>
                            <li>A daily text with a list of news articles concerning COVID-19</li>
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

<style>
.card {
  background-color: rgb(245, 245, 245, .9);
  border: 1px solid lime;
  margin-top: 25%;
}

.btn-success {
    border: 1px solid black;
    border-radius: 10px;
}
</style>
