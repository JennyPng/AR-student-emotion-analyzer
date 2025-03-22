using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

public class ApiClient : MonoBehaviour
{
    private string serverUrl = "https://mako-pleasing-filly.ngrok-free.app/data"; // Ngrok URL
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
