using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.UI;
using NetMQ;
using NetMQ.Sockets;
using System.Linq;
using System;
using System.IO;
using System.IO.Compression;
using Newtonsoft.Json;

[RequireComponent(typeof(Camera))]


public class CameraScript : MonoBehaviour
{
	Camera snapCam;
    // ZeroMQ socket for sending data
    PublisherSocket socket;

    int resWidth = 640;
    int resHeight = 480;

    void Awake()
    {
        snapCam = GetComponent<Camera>();
        if (snapCam.targetTexture == null)
        {
            snapCam.targetTexture = new RenderTexture(resWidth, resHeight, 24);
        }
        else
        {
            resWidth = snapCam.targetTexture.width;
            resHeight = snapCam.targetTexture.height;
        }
        socket = new PublisherSocket();
        socket.Bind("tcp://*:5555");
    }

    public void CallTakeSnapshot()
    {
        snapCam.gameObject.SetActive(true);
    }

    public void LateUpdate()
    {

        Texture2D snapshot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
        snapCam.Render();
        RenderTexture.active = snapCam.targetTexture;

        snapshot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);

        // Convert the webcam data to a byte array andf send it using the ZeroMQ socket
        Color32[] pixels = snapshot.GetPixels32();
        // load the pixels into a byte array
        byte[] buffer = new byte[pixels.Length * 4];

        for (int i = 0; i < pixels.Length; i++)
        {
            Color32 c = pixels[i];
            buffer[i * 4] = c.r;
            buffer[i * 4 + 1] = c.g;
            buffer[i * 4 + 2] = c.b;
            buffer[i * 4 + 3] = c.a;
        }
        Debug.Log(buffer.Length);

        using (MemoryStream ms = new MemoryStream())
        {
            using (GZipStream gzip = new GZipStream(ms, CompressionMode.Compress))
            {
                gzip.Write(buffer, 0, buffer.Length);
            }
            byte[] compressedImageData = ms.ToArray();

            socket.SendFrame(compressedImageData);
        }

        // Debug.Log("Sent data" + buffer.Length);
    }
}

		