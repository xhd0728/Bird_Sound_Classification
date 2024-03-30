<template>
  <div class="main">
    <div class="h-14 p-3 flex justify-between w-full border-b bg-white opacity-80">
      <div class="text-xl text-blue-400" style="margin:auto">基于音频特诊分析的动态鸟类识别分析与百科</div>
    </div>

    <div class="flex justify-center mt-8">
      <div class="flex">
        <div class="bg-white p-8 rounded-md w-27rem">
          <div class="flex items-center w-full">
            <!-- <img :src="request.baseURL + imageUrl" alt /> -->
          </div>

          <el-upload class="upload-demo" drag ref="upload" :http-request="upload" action="#" :auto-upload="false"
            :show-file-list="true" :limit="1">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或
              <em>点击上传</em>
            </div>
          </el-upload>


          <button class="mybtn mt-8" @click="submitUpload">Upload</button>
        </div>
        <!-- <div class="ml-8 w-27rem bg-white rounded-md p-4" v-loading="timer"
          element-loading-text="受限于cpu服务器算力，运算时间可能较长，请耐心等待..." element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.7)">
          <div v-if="result && !timer" class="flex items-center h-full">
            <img :src="result" alt />
          </div>
        </div> -->
        <div class="ml-8 w-27rem bg-white rounded-md p-4" v-loading="uploaded && timer" element-loading-text="正在计算中..."
          element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.7)">
          <div v-if="!timer">
            <div class=" bird-name text-2xl text-indigo-500">英文名：{{ name_list_en[0]}}</div>
            <div class=" bird-name text-2xl text-indigo-500">中文名：{{ name_list_cn[0] }}</div>
            <div id="bird_img">
              <img :src="birdimg_url" alt="">
            </div>
            <div id="bird_html" class="text-blue-700 text-xl font-bold">
              <a :href="bird_html"   target="_blank">点击查看该品种鸟的详情</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="body">
      <div ref="myimg" class="ppt" style="position: relative;" v-if="!timer">
        <img :src="'data:audio/image;base64,'+ bird_ppt" alt="" @click="change_time($event)">
        <div id="playerMarker" :style="{ 'left': playMaker_left + 'px' }" v-if="!timer"></div>
      </div>



      <div class="mp3"  v-if="!timer">
        <audio ref="audioplayer" :src="'data:audio/wav;base64,'+ base_64"  controls id="player" @timeupdate="setplayMaker()">
        <source  />
        </audio>
      </div>
      <div ref="echarts" id="echarts" >  
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
  },
  data() {
    return {
      uploaded: false,
      timer: true,
      name_list_cn:[],
      name_list_en:[],
      value_list:[],
      base_64:'',
      birdimg_url:'',
      bird_html:'',
      bird_ppt:'',
      playMaker_left: 0,
      now_charts_data:{
        text:'Predicted Scores Of Top Ten',
        series:[],
        yAxis:[],
      },
      file_name:'',
    };
  },
  methods: {
  
    drawCharts()
    {
      var myChart = this.$echarts.init(this.$refs.echarts)
      myChart.setOption({
        title:{
          text:this.now_charts_data.text,
          x:'center',
          y:'20px',
        },
        tooltip: {trigger: 'axis'},
        legend:{
          data:['得分'],
          x:'right',      //可设定图例在左、右、居中
          y:'20px'
        },
        xAxis:[
          {
            type:'value',
            boundaryGap: [0, 0.01],
            axisLabel: {
               show: true,
               textStyle: {
                    color: '#c3dbff',  
                    fontSize : 16      
              }
            }
          }
        ],
        yAxis:[
          {
            type: 'category',
            inverse:true,
            data: this.now_charts_data.yAxis,  //纵坐标以数组形式存储字符串
            axisLabel: {
               show: true,
               textStyle: {
                    color: '#c3dbff',  
                    fontSize : 16      
              }
            }
          },
        ],
        series:[
          {
            name:'得分',
            type:'bar',
            data:this.now_charts_data.series, //横坐标以数组存储得分
            itemStyle:{
              normal:{
                color:'black'
              }
            }
          }
        ]
      })
    },
    change_time(e) {
      let x = e.offsetX;
      this.playMaker_left = x;
      const audioPlayer = this.$refs.audioplayer;
      const duration = audioPlayer.duration;
      this.$refs.audioplayer.currentTime = x / 1100 * duration;
    },
    setplayMaker() {
      const audioPlayer = this.$refs.audioplayer;
      const currentTime = audioPlayer.currentTime;
      const duration = audioPlayer.duration;
      const progress = currentTime / duration;
      this.playMaker_left = progress * 1100;
    },
    upload(e) {
      console.log(e)
      console.log(1111);
      let form = new FormData();
      form.append('file', e.file);
      this.file_name=e.file.name;
      // console.log(this.file_name.substring(0,this.file_name.lastIndexOf(".")));
      
      this.uploaded = true;
      this.timer=true;
      this.request.instance.post('/api/v1/audio/upload', form).then((res) => {
        
        this.name_list_cn=res.data.name_list_cn,
        this.now_charts_data.yAxis=this.name_list_cn,
        this.name_list_en=res.data.name_list_en,
        this.value_list=res.data.value_list,
        this.now_charts_data.series=this.value_list,

        this.request.instance({
          method:'GET',
          url:'/api/v1/audio/audioB64',
          params:{
            name:this.file_name,
          }
        }).then((res)=>{
          this.base_64=res.data.data;
        });
        this.request.instance({
          method:'GET',
          url:'/api/v1/audio/info',
          params:{
            name:this.name_list_en[0]
          }
        }).then((res)=>{
          this.birdimg_url=res.data.data[0].image_link;
          this.bird_html=res.data.data[0].wiki_link;
        });
        this.request.instance({
          method:'GET',
          url:'/api/v1/audio/imageB64',
          params:{
            name:this.file_name
          }
        }).then((res)=>{
          this.bird_ppt=res.data.data;
        })
        this.timer=false;
        this.$refs.upload.clearFiles();
        this.drawCharts();
        
      
      })



    },
    submitUpload() {
      if (this.$refs.upload.uploadFiles.length) {
        this.$refs.upload.submit();
      } else {
        this.$message({
          showClose: true,
          message: '请先上传待识别音频',
          type: 'error'
        });
      }

    },
  },
};
</script>

<style>
.main {
  height: 165vh;
  /* background: linear-gradient(45deg, #18cde2, #f21bff); */
  background-image: url(../../public/images/bgc6.png);
  /* background-size: 1300px 1000px; */
  background-repeat: no-repeat;
  /* background-position-x: center; */
  /* background-position-y:400px ; */
  background-size: contain;
}

.w-27rem {
  width: 27rem;
}

.bird-name {
  text-align: center;
}
#bird_img{
  width: 200px;
  height: 200px;
  /* background-color: skyblue; */
  margin: auto;
  overflow: hidden;
}
#bird_img img{
  height: 100%;
  width: auto;
  display: block;
  background-size: contain ;
  margin: auto;
}
#bird_html{
  margin-top: 25px;
  text-align: center;
}
.body {
  width: 1100px;
  margin: auto;
  margin-top: 30px;
}

.ppt {
  width: 100%;
  height: 150px;
  user-select: none;
  margin-bottom: 30px;
}

.ppt img {
  overflow-clip-margin: content-box;
  overflow: clip;
  height: 100%;
  cursor: pointer;
}

#playerMarker {
  display: block;
  position: absolute;
  top: 0px;
  width: 3px;
  height: 150px;
  background-color: deepskyblue;
}

#player {
  width: 100%;
}
#echarts{
  width:1100px;
  height: 500px;
}

/* webkit浏览器 */
audio::-webkit-progress-value {
    background-color: black;
  }
  /* firefox浏览器 */
  audio::-moz-progress-bar {
    background-color:skyblue;
  }
</style>
