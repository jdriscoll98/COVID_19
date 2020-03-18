<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card card-block pl-5 pr-5 pt-3 pb-3">
                    <h5 class="text-center bold">Your phone number has now been verified. <br /> Thank you!</h5>
                    <h6 class="text-center secondary">You will receive a text shortly to set up your account</h6>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ThankYou'
}
</script>

<style scoped>
.card {
  background-color: rgb(245, 245, 245, .9);
  border: 1px solid lime;
  margin-top: 25%;
}
.bold {
    font-weight:800;
}
.secondary {
    font-weight:400;
}

</style>
