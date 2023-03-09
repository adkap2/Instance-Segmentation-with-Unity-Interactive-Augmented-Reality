<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/adkap2/Instance-Segmentation-with-Unity-Interactive-Augmented-Reality?style=for-the-badge)
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This document outlines the steps to use Yolact, a fully convolutional model for real-time instance segmentation, on a custom dataset for processing indoor environments. The dataset is synthetically generated using Unity's SyntheticHome application and requires modifications to various training files, along with a pretrained weights file. Mean Average Precision (mAP) is the primary precision metric used for training and evaluation.

Additionally, this readme provides instructions for installing and using Unity's VirtualHome program, which simulates multi-agent tasks in home-like environments. The readme also includes details on the Unity Synthetic Homes dataset generator, which produces photorealistic images for use with computer vision models, and FiftyOne, an open-source tool used for curating and modifying image datasets for training computer vision models.

## IP Socket Communication

To perform real-time object detection and segmentation on frames generated within the Unity VirtualHome environment, I utilized IP socket communication with the NetMQ Library to exchange data between the C# (Unity) VirtualHome Application and a Python (Yolact_Edge) program. I added a script to the (Unity) Virtual Agents application to capture each frame and send them over the socket to the Yolact_Edge inferencing program for processing.

To optimize the transfer of data, I implemented file compression using the GZIP algorithm before sending each frame over the socket. This reduced the size of the data being transferred, resulting in faster processing times and reduced bandwidth requirements.

The IP socket communication was implemented using the TCP/IP protocol, which ensured reliable and ordered data transfer between the two applications. The C# application acted as the client, while the Python application acted as the server, listening for incoming data on a specified port.

Once the Yolact_Edge inferencing program received the compressed frame over the socket, it decompressed the data, performed instance segmentation using the specified YolactEdge trained weights and object classes. Then, using OpenCV, it rendered the results within a generated window. 

Overall, the use of IP socket communication and file compression enabled efficient and seamless communication between the two applications, facilitating real-time inference from frames generated within the Unity VirtualHome environment.
eal-time instance segmentation inference was performed within the Unity VirtualHome Environment

#### The GIFs below display each frame generated from the Unity VirtualHome Environment, after undergoing real-time instance segmentation inference and post-processing.


<table>
  <tr>
    <td align="center" style="padding: 10px;">
      <img src="videos/coco_trained_model.gif" alt="YOLACT pretrained model from COCO Dataset" width="400" height="350"><br>
      YOLACT pretrained model from the COCO Dataset
    </td>
    <td align="center" style="padding: 10px;">
      <img src="videos/adam_trained_original.gif" alt="Custom trained model from Synthetic Indoor Home environment dataset" width="400" height="350"><br>
      Custom trained model from a Synthetic dataset
    </td>
  </tr>
</table>

### Notes on the Trained Models:



### Built With

This section lists major frameworks and libraries that were used to create the project. The following plugins were used:


* [![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white)](https://opencv.org/)
  - Open-source computer vision and machine learning software library
* [![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)
  *  Open-source deep learning framework used for computer vision tasks
* [![Unity](https://img.shields.io/badge/Unity-000000?style=for-the-badge&logo=Unity&logoColor=white)](https://unity.com/)
  * Cross-platform game engine used for developing 2D and 3D games and simulations
* [![Unity Virtual Home](https://img.shields.io/badge/Unity_Virtual_Home-003146?style=for-the-badge&logo=Unity&logoColor=white)](https://www.virtual-home.org/)
  * Research platform for simulating domestic environments with a variety of interactive objects

* [![Unity Perception](https://img.shields.io/badge/Unity_Perception-000000?style=for-the-badge&logo=unity&logoColor=white)](https://docs.unity3d.com/Packages/com.unity.perception@1.0/manual/index.html)
  * Computer vision and machine learning toolkit for Unity used for developing perception-driven applications
* [![FiftyOne](https://img.shields.io/badge/FiftyOne-008CBA?style=for-the-badge&logo=fiftyone&logoColor=white)](https://voxel51.com/fiftyone/)
  * Python package for exploring and analyzing computer vision datasets
* [![YOLACT](https://img.shields.io/badge/YOLACT-FFA500?style=for-the-badge&logo=yolact&logoColor=white)](https://github.com/dbolya/yolact/)
  * Real-time instance segmentation algorithm that detects and segments objects in images and videos
* [![YOLACTEdge](https://img.shields.io/badge/YOLACTEdge-4B0082?style=for-the-badge&logo=yolactedge&logoColor=white)](https://github.com/razorx89/YOLACTEdge/)
  * Lightweight version of YOLACT that is optimized for edge devices and embedded systems
* [![ZeroMQ](https://img.shields.io/badge/ZeroMQ-D91E18?style=for-the-badge&logo=ZeroMQ&logoColor=white)](https://zeromq.org/)
  * High-performance asynchronous messaging library that facilitates communication between distributed applications



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To recreate the project, follow the instructions located in the documents folders. The documents folder contains the following files:

* [Synthetic Homes Data Generation](documentation/SyntheticHomes_Data_Generator_README.pdf)
* [Yolact Install and Usage](documentation/Yolact_Training_README.pdf)
* [Fiftyone Installations and Usage](documentation/FiftyOne_README.pdf)
* [Unity Virtual Home Installations and Usage](documentation/Unity_Virtual_Home_README.pdf)

### Prerequisites

* <font size = "4"> Computer Specifications</font>
  * Intel i5 9600k
  * GTX 1080 ti (11gb ram)
  * 32gb memory
* <font size = "4">Operating System</font>
  * Ubuntu 20.04
  * Windows 10


### Installation


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.



<!-- ROADMAP -->
## Roadmap
- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Add "frequently asked questions" document
- [ ] 

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Email - [@adkap2](mailto:adkap2@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

```markdown

```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge


[contributors-url]: https://github.com/adkap2/Instance-Segmentation-with-Unity-Interactive-Augmented-Reality/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/adam-goldstein123/
[product-screenshot]: images/screenshot.png
