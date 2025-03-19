using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

public class ApiClient : MonoBehaviour
{
    private string serverUrl = "https://bluejay-novel-ghoul.ngrok-free.app/data"; // Ngrok URL
    private TextManager textManager;

    // Start is called before the first frame update
    void Start()
    {
        textManager = TextManager.Instance;
        StartCoroutine(GetData());
    }

    IEnumerator GetData()
    {
        while (true)
        {
            using (UnityWebRequest request = UnityWebRequest.Get(serverUrl))
            {
                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.ConnectionError ||
                    request.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.LogError("Error: " + request.error);
                }
                else
                {
                    try
                    {
                        string jsonString = request.downloadHandler.text;
                        ConfusionData confusionData = JsonConvert.DeserializeObject<ConfusionData>(jsonString);

                        Debug.Log($"Confusion Level: {confusionData.confusion}");
                        foreach (string topic in confusionData.confusing_topics)
                        {
                            Debug.Log($"Confusing Topic: {topic}");
                        }

                        // Update the UI through the TextManager
                        if (confusionData != null)
                        {
                            textManager.updateConfusionData(confusionData);
                        }
                    }
                    catch (JsonException e)
                    {
                        Debug.LogError($"JSON parsing error: {e.Message}");
                    }
                }
            }
        }
    }
}


//// Unity Client (Unity C# Script - Attach to a GameObject)
//using System;
//using System.Net.Sockets;
//using System.Text;
//using System.Threading;
//using UnityEngine;
//using System.Collections.Generic;
//using Newtonsoft.Json;
//using System.Collections; // Install via Unity Package Manager: Newtonsoft Json

//public class SocketClient : MonoBehaviour
//{

//    //public string serverIP = "10.18.156.162";
//    //public string serverIP = "205.175.106.52"; // 
//    public string serverIP = "172.20.10.3"; // MINE ON HOTSPOT

//    //public string serverIP = "10.19.108.229"; // brians
//    //public string serverIP = "172.20.10.2"; // brians on my hotspot

//    public int serverPort = 65432;

//    private TcpClient client;
//    private NetworkStream stream;

//    private bool isRunning;

//    private TextManager textManager;

//    void Start()
//    {
//        textManager = TextManager.Instance;
//        ConnectToServer();
//    }

//    void ConnectToServer()
//    {
//        try
//        {
//            client = new TcpClient(AddressFamily.InterNetwork);
//            client.Connect(serverIP, serverPort);

//            stream = client.GetStream();
//            isRunning = true;

//            StartCoroutine(ReceiveData());
//        }
//        catch (Exception e)
//        {
//            Debug.LogError("Socket error: " + e);
//            Invoke(nameof(ConnectToServer), 3f);
//        }
//    }

//    IEnumerator ReceiveData()
//    {
//        byte[] receiveBuffer = new byte[1024];
//        StringBuilder stringBuilder = new StringBuilder(); // Buffer for incomplete JSON

//        while (isRunning)
//        {
//            try
//            {
//                int bytesRead = stream.Read(receiveBuffer, 0, receiveBuffer.Length);
//                if (bytesRead > 0)
//                {
//                    string receivedData = Encoding.UTF8.GetString(receiveBuffer, 0, bytesRead);
//                    stringBuilder.Append(receivedData);

//                    string data = stringBuilder.ToString();

//                    if (data.Contains("\n")) // Check for end of JSON
//                    {
//                        string[] jsonStrings = data.Split('\n', StringSplitOptions.RemoveEmptyEntries);
//                        foreach (string jsonString in jsonStrings)
//                        {

//                            try
//                            {
//                                ConfusionData confusionData = JsonConvert.DeserializeObject<ConfusionData>(jsonString);

//                                Debug.Log("received: " + confusionData.confusion.ToString());

//                                if (confusionData != null)
//                                {
//                                    textManager.updateConfusionData(confusionData);
//                                }

//                                stringBuilder.Clear(); // Clear the buffer
//                            }
//                            catch (JsonException e)
//                            {
//                                Debug.LogError("JSON parsing error: " + e);
//                                // Handle the error, potentially by waiting for more data
//                            }
//                        }
//                    }

//                }
//            }
//            catch (SocketException socketException)
//            {
//                Debug.LogError("Socket exception: " + socketException);
//                break;
//            }
//            catch (System.IO.IOException ioException)
//            {
//                Debug.LogError("IO exception: " + ioException);
//                break;
//            }
//            catch (Exception e)
//            {
//                Debug.LogError("Receive error: " + e);
//                break;
//            }
//        }
//        yield return null;
//    }

//    void Update()
//    {

//    }
//}