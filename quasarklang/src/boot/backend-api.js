import axios from "axios";
axios.defaults.headers.post["Content-Type"] = "multipart/form-data";
// import VueCookies from "vue-cookies";
// VueCookies.config("7d");

const API = axios.create({
  // baseURL: 'https://arboratorgrew.ilpga.fr:8888/api',
  // baseURL: `/api`,
	// baseURL: process.env.DEV ? "http://127.0.0.1:8000/api" : process.env.API + "/api",
	baseURL: process.env.DEV ? 'http://localhost:8000'  : process.env.API ,
	// + "/api"
	timeout: 50000,
	withCredentials: true,
});

// const AUTH = axios.create({
//   // baseURL: 'https://arboratorgrew.ilpga.fr:8888/login',
//   // baseURL: process.env.API + `/login`,
//   baseURL: process.env.DEV ? "/login" : process.env.API + "/login",
//   timeout: 5000,
//   withCredentials: true,
// });


export default {
  // ---------------------------------------------------- //
  // ---------------        Project       --------------- //
  // ---------------------------------------------------- //
	getAllConlls() {
		return API.get("api/serveconll");
	},
	getConll(name) {
		// console.log(99999,name)
		return API.post("api/serveconll", { name: name });
	},


};
