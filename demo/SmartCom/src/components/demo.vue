<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div id="inputtext">
      <input v-model="name" placeholder="input username...">
      <p>username is : {{name}} </p>
      <button type="button" @click="submit">添加用户</button>
      <p>User ID is : {{userid}} </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'demo',
  data () {
    return {
      msg: '数据库演示样例！',
      name: "",
      userid: ""
      // user_id: get(api_base+'db_serch/?name=admin').resolve.id
    }
  },
  methods : {
    submit() {
      console.log(this.name);
      axios.post('/api/db_insert/',{"name":this.name});
      // var X = axios.get('/api/db_search/',{"name":this.name}).then(res => this.userid=res)
      // console.log(X);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
