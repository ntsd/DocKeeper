<template>
  <div class="canvasBox" style="
 width: 100%;height: 100%;">
    <canvas id="canvas" v-on:mousedown="handleMouseDown" v-on:mouseup="handleMouseUp" v-on:mousemove="handleMouseMove"
            style="
         border: solid 1px blue;
         width:100%;" ></canvas>
  </div>
</template>

<script>
  export default {
    props: {
      imagesrc:'',
      linesX:null
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
      }
    },
    computed: {
    },
    methods: {
      handleMouseDown: function (event) {
        this.mouse.down = true;
      },
      handleMouseUp: function () {
        this.linesX.push(this.lineX)
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
      const linesX = this.linesX
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
      }
      this.img.src = this.imagesrc
    }
  }
</script>
