<template>
  <div class="canvasBox" style="
 width: 100%;height: 100%;">
    <canvas id="canvas" v-on:mousedown="handleMouseDown" v-on:mouseup="handleMouseUp" v-on:mousemove="handleMouseMove"
            oncontextmenu='return false;'    @keydown.native.ctrl.86="ctrlDown" style="
         border: solid 1px blue;
         width:100%;" ></canvas>
  </div>
</template>

<script>
  export default {
    props: {
      imagesrc:'',
      tableData:{
        linesX:null,
        lineY:0
      }
    },watch: {
      imagesrc: function(newVal, oldVal) {
        this.img.src = newVal
      }
    },
    data: function () {
      return {
        mouse: {
          current: {
            x: 0,
            y: 0
          },
          down: false
        },
        img:null,
        lineX:null,
        mouseY:null
      }
    },
    computed: {
    },
    methods: {
      ctrlDown: function (event) {
        console.log('ctrl')
        console.log(event)
      },
      handleMouseDown: function (event) {
        // console.log(event)
        this.mouse.down = true;
      },
      handleMouseUp: function (event) {
        // console.log(event)
        if(event.button == 0){
          this.tableData.linesX.push(this.lineX)
          var c = document.getElementById("canvas");
          var ctx = c.getContext("2d");
          // ctx.setLineDash([6]); // no need cuz already set in mounted
          // ctx.lineWidth = Math.round(this.width/400);
          // ctx.strokeStyle ='#ff0000'
          ctx.moveTo(this.lineX,0);
          ctx.lineTo(this.lineX,this.img.height);
          ctx.stroke();
          this.mouse.down = false;
          //console.log(this.linesX)
        }
        if(event.button == 2){
          this.tableData.lineY = this.mouseY
          var c = document.getElementById("canvas");
          var ctx = c.getContext("2d");
          ctx.moveTo(0,this.mouse.current.y);
          ctx.lineTo(this.img.width,this.mouse.current.y);
          ctx.stroke();
          // console.log(this.lineY)
        }
      },
      handleMouseMove: function (event){
        var c = document.getElementById("canvas");
        var rect = c.getBoundingClientRect();
        var scaleX = c.width / rect.width;    // relationship bitmap vs. element for X
        var scaleY = c.height / rect.height;  // relationship bitmap vs. element for Y

//        use event.clientX not event.pageX
        this.mouse.current = {
          x: (event.clientX - rect.left) * scaleX,
          y: (event.clientY - rect.top) * scaleY
        }
        this.lineX = this.mouse.current.x
        this.mouseY = this.mouse.current.y
        // this.mouseY = this.mouse.current.y
        // var ctx = c.getContext("2d");  // can't do real time show line
        // ctx.drawImage(this.img,0,0)
        // this.linesX.forEach((lineX) => {
        //   ctx.moveTo(lineX,0);
        //   ctx.lineTo(lineX,this.img.height);
        //   ctx.stroke();
        // })
        // ctx.moveTo(this.lineX,0);
        // ctx.lineTo(this.lineX,this.img.height);
        // ctx.stroke();
      }
    },
    beforeMount() {

    },
    mounted() {
      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");
      ctx.translate(0.5, 0.5);
      ctx.imageSmoothingEnabled= false;
      const linesX = this.tableData.linesX
      const lineY = this.tableData.lineY
      this.img = new Image
      this.img.onload = function(){
        c.width = this.width
        c.height = this.height
        ctx.drawImage(this,0,0)
        ctx.setLineDash([6]);
        ctx.lineWidth = Math.round(this.width/400);
        ctx.strokeStyle ='#ff0000'
        linesX.forEach((lineX) => {
          ctx.moveTo(lineX,0);
          ctx.lineTo(lineX,this.height);
          ctx.stroke();
        })
        ctx.moveTo(0,lineY);
        ctx.lineTo(this.width,lineY);
        ctx.stroke();
      }
      this.img.src = this.imagesrc
    }
  }
</script>
