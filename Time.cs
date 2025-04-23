    using UnityEngine;
    using UnityEngine.SceneManagement;
    using TMPro;

    public class Timer : MonoBehaviour
    {
    int je = 0;
    public int cas;
    public float speed;
    TextMeshProUGUI text; 

        void Start() {
            text = gameObject.GetComponent<TextMeshProUGUI>();
        }

    void Timr() {
        cas--;
        je = 0;
    }

    void Update() {
        text.text = (cas/60).ToString() + " : " + (cas%60).ToString();
        
        if(je == 0) {
            je = 1;
            Invoke("Timr", speed);
        }

        if(cas == 0) {
            //..load end in prikazi score
        }
    }
    }