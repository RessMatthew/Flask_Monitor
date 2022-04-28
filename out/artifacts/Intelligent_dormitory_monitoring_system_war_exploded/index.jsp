<%--
  Created by IntelliJ IDEA.
  User: wgj
  Date: 2022/4/27
  Time: 23:00
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>

  <link rel="stylesheet" href="css/login.css">
</head>
  <body>
  <div class="container">
    <div class="form-box">
      <!-- 注册 开始 -->
      <div class="register-box ">
        <h1>register</h1>
        <input type="text" placeholder="用户名" />
        <input type="email" placeholder="邮箱" />
        <input type="password" placeholder="密码" />
        <input type="password" placeholder="确认密码" />
        <button>注册</button>
      </div>
      <!-- 注册 结束 -->

      <!-- 登录盒子 开始 -->
      <div class="login-box hidden">
        <h1>login</h1>
        <input type="text" placeholder="用户名">
        <input type="password" placeholder="密码">
        <button>登录</button>
      </div>
      <!-- 登录盒子 结束 -->
    </div>

    <div class="con-box left">
      <h2>欢迎来到
        <span>宠物之家</span>
      </h2>
      <p>快来领取你的专属
        <span>宠物</span>吧
      </p>
      <img src="images/1.jpg" alt="525">
      <p>已有账号</p>
      <button id="login">去登录</button>
    </div>

    <div class="con-box right">
      <h2>欢迎来到<span>宠物之家</span></h2>
      <p>快来领取你的专属<span>宠物</span>吧</p>
      <img src="images/02.jpg" alt="522">
      <p>没有账号</p>
      <button id="register">去注册</button>
    </div>
  </div>



  <script>
    let login = document.getElementById('login');

    let register = document.getElementById('register');
    let form_box = document.getElementsByClassName('form-box')[0];
    let register_box = document.getElementsByClassName('register-box')[0];
    let login_box = document.getElementsByClassName('login-box')[0];

    register.addEventListener('click', () => {
      console.log('点击了注册事件');
      form_box.style.transform = 'translateX(80%)';
      login_box.classList.add('hidden');
      register_box.classList.remove('hidden');
    })

    login.addEventListener('click', () => {
      console.log('点击了登录事件');
      form_box.style.transform = 'translateX(0%)';
      register_box.classList.add('hidden');
      login_box.classList.remove('hidden')
    })
  </script>
  </body>
</html>
