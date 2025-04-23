using UnityEngine;
using TMPro;

public class Skore : MonoBehaviour
{
    public int score = 0;
    TextMeshProUGUI text; 

    void Start() {
        text = gameObject.GetComponent<TextMeshProUGUI>();
    }

    void Update() {
        text.text = "Score: " + score.ToString();
    }
}