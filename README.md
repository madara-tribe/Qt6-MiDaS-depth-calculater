# Simurate Jetson ONNX 3dDepth Calcurator advanced

Use onnx yolov7-tiny and midas-onnx model to calcurate 3d depth distance with camera on Qt6.
It simurate to estimate distances as car driving camera depth estimate system.

<b>avarage inference time (midas + yolov7)</b>
```txt
760.16 [ms]
```


## area to estimate distance in this movie 

you can not adapt this calcuration to <b>「Out of area」</b>

<img src="https://github.com/madara-tribe/Qt6-MiDaS-depth-calculater/assets/48679574/4d0b30f1-246a-4e44-93f1-f536951ccbde" width="600px" height="300px">



## 3D distance calcurate formula 



<b>Sample driving movie</b>
- [sample driving movie](https://drive.google.com/file/d/18P0mS9fjMD1nq2tKMzD-u_eXjpjttJ4n/view?usp=sharing)


  

<b>Inference GIF</b>

<img src="https://github.com/madara-tribe/Qt6-MiDaS-depth-calculater/assets/48679574/0143b8eb-464a-4d92-8e27-d37a9bc0ec58" width="600px">


# References
- [Getting Started with Depth Estimation using MiDaS and Python](https://medium.com/artificialis/getting-started-with-depth-estimation-using-midas-and-python-d0119bfe1159)
