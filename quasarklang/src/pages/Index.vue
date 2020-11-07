<template>
  <q-page class="full-width row wrap justify-start items-start content-start">


      <!-- <audio controls="controls" id="audio_player">
    <source src="/enregistrement_sonore_Richard_Matthieu.ogg" type="audio/ogg" />
    <source src="/enregistrement_sonore_Richard_Matthieu.mp3" type="audio/mpeg" />
    Your browser does not support the audio element.
  </audio> -->
    <!-- <img
      alt="Quasar logo"
      src="~assets/quasar-logo-full.svg"
    > -->
<!-- :canv-fill-color='"black"'
:canv-width="canvwidth"
    :canv-width="1500"
    width="2500px"
    style="display:block"
     -->
 &nbsp;
    <q-separator spaced />
     &nbsp;

    <div class="row q-col-gutter-md">
      <!-- <div class="col-4" v-for="n in 25" :key="`md-${n}`"> -->
        <div clickable v-ripple v-for="(f,i) in conlls" :key="f" style="min-width:300px">
          <div><q-btn no-caps color="primary" :label="i+'. '+f"  icon="music_note"  :to="'/conlls/'+f" /></div>
        </div>
      <!-- </div> -->
    </div>
<q-separator spaced />
    
       
     
      &nbsp;
     </q-card>
      <q-btn no-caps
          round
          @click="btnClick"
          color="primary text-white"
        >test
          <q-tooltip
            content-class="bg-primary"
            content-style="font-size: 16px"
            >useless button for testing</q-tooltip>
        </q-btn>
        <!-- <av-line v-if="waveWidth > 0" ref-link="player" :canv-width="waveWidth"/> -->
<!-- <audio ref="foo" src="/enregistrement_sonore_Richard_Matthieu.mp3"></audio>
<av-bars ref-link="foo" />
<av-line ref-link="foo" /> -->
    <!-- <av-media
      :media="mediaObject"
    ></av-media> -->

  </q-page>
</template>

<script>
import Vue from 'vue'
import api from '../boot/backend-api';

// import AudioVisual from 'vue-audio-visual'

// Vue.use(AudioVisual)
export default {
  name: 'PageIndex',
  data() {
    return {
      // audioplayer: null,
      conlls: [],
      mediaObject:"/enregistrement_sonore_Richard_Matthieu.mp3",
      waveWidth:2500,
      cc:false,
      currentTime:121,
      canvwidth:0,
    }
  },
  created() {
    console.log(7878,window.innerWidth)
    this.waveWidth = window.innerWidth
  },
  mounted() {
     this.getAllConlls()
  //  this.waveWidth = this.$refs.p.clientWidth;
  //  console.log(2323,this.$refs.p)
  // Assign an ontimeupdate event to the <video> element, and execute a function if the current playback position has changed
    // this.audioplayer = this.$refs.player.audio;
    // this.$refs.player.audio.ontimeupdate = () => this.onTimeUpdate();
    // this.canvwidth=2000;
  },
  methods: {
    btnClick(a,b) {
      // console.log(78787,a,b, this.currentTime)
      this.getAllConlls()
  
    //   console.log(this.$refs.player.audio.play())
    //   this.$refs.player.audio.currentTime=77;
 
    },
    /**
		 * Retrieve conll files from backend 
		 * 
		 * @returns void
		 */
		getAllConlls(){ 
      console.log('getAllConlls',8787878)
			api.getAllConlls()
			.then( response => {  
        console.log(4444,response.data.conlls)
        this.conlls = response.data.conlls;
			})
			.catch(error => { 
        console.log(4444,error)
				// this.$store.dispatch("notifyError", {error: error});
			});
		}
  }
}
</script>
