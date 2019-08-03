const app = getApp()
Component({
  properties: {
    navbarData: {   //navbarData   由父页面传递的数据，变量名字自命名
      type: Object,
      value: {},
      observer: function (newVal, oldVal) { }
    }
  },
  data: {
    
  // 导航栏标题
    nvabarData: {
    showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
    title: '原地起飞', //导航栏 中间的标题
  },

    height: '',
    //默认值  默认显示左上角
    navbarData: {
      showCapsule: 1
    }
  },
  attached: function () {
    // 获取是否是通过分享进入的小程序
    this.setData({
      share: app.globalData.share
    })
    // 定义导航栏的高度   方便对齐
    this.setData({
      height: app.globalData.height
    })
  },
  methods: {
    // 返回上一页面
    _navback() {
      wx.navigateBack()
    },
    //返回到首页
    _backhome() {
      wx.redirectTo({
        url: '/pages/home_page/home_page',
      })
    }
  }

})