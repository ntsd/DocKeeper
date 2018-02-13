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
      rect:{
        x:0,
        y:0,
        w:0,
        h:0
      }
    },
    data: function () {
      return {
        mouse: {
          current: {
            x: 0,
            y: 0
          },
          previous: {
            x: 0,
            y: 0
          },
          down: false
        },
        img:null
      }
    },
    computed: {
//      currentMouse: function () {
//        var c = document.getElementById("canvas");
//        var rect = c.getBoundingClientRect();
//
//        return {
//          x: this.mouse.current.x - rect.left,
//          y: this.mouse.current.y - rect.top
//        }
//      }
    },
    methods: {
      draw: function (event) {
        if (this.mouse.down ) {
          var c = document.getElementById("canvas");
          var ctx = c.getContext("2d");
          ctx.drawImage(this.img,0,0)//, c.width, c.height * this.img.height / this.img.width);  // ctx.clearRect(0,0,800,800);
          ctx.setLineDash([6]);
         // console.log('line width',this.img.width,Math.round(this.img.width/400))
          ctx.lineWidth = Math.round(this.img.width/400);
          ctx.strokeStyle ='#ff0000'
          ctx.strokeRect(this.rect.x, this.rect.y, this.rect.w, this.rect.h);
        }

      },
      handleMouseDown: function (event) {
        this.mouse.down = true;
//        this.mouse.current = {
//          x: event.pageX,
//          y: event.pageY
//        }
        this.rect.x = this.mouse.current.x;
        this.rect.y = this.mouse.current.y;


      },
      handleMouseUp: function () {
        this.mouse.down = false;
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
       // console.log(this.mouse.current.x, this.mouse.current.y)
        if (this.mouse.down) {
          this.rect.w = this.mouse.current.x - this.rect.x;
          this.rect.h = this.mouse.current.y - this.rect.y ;
          // ctx.clearRect(0,0,canvas.width,canvas.height);
          this.draw(event)
        }
        // this.draw(event)

      }
    },
    beforeMount() {

    },
    mounted() {
      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");
      ctx.translate(0.5, 0.5);
      ctx.imageSmoothingEnabled= false;
      // var img = document.getElementById("imageRef");
      const rect = this.rect // for use in onload function
      this.img = new Image
      this.img.onload = function(){
        c.width = this.width
        c.height = this.height
        //console.log(c.width, c.height)
        ctx.drawImage(this,0,0)//, c.width, c.height * img2.height / img2.width)
        //draw init line when get load
        ctx.setLineDash([6]);
        ctx.lineWidth = Math.round(this.width/400);
        ctx.strokeStyle ='#ff0000'
        ctx.strokeRect(rect.x, rect.y, rect.w, rect.h);
      }
      this.img.src = this.imagesrc

      // resize after window update
      // console.log(this.$el)
      // window.addEventListener("resize", updateCanvas);
      // function updateCanvas() {
      //   console.log('resize',c.width, c.height, window.innerWidth, window.innerHeight)
      //   // c.width = this.$el.offsetWidth;//window.innerWidth;
      //   // c.height = this.$el.offsetHeight;//window.innerHeight;
      //   ctx.drawImage(img2,0,0, c.width, c.height * img2.height / img2.width)
      // }
      // updateCanvas();
    }
  }
</script>
