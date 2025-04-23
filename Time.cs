using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

public class Timer : MonoBehaviour
{
   int je = 0;
   public int cas;
   public float speed;
   TextMeshProUGUI text; 
   private int temp;

    void Start() {
        TextMeshProUGUI text = gameObject.GetComponent<TextMeshProUGUI>();
    }

   void Timr() {
    cas--;
    je = 0;
   }

   void Update() {
    text.text = (cas/60).ToString() + " : " + (cas%60).ToString();
    if(cas % 60 > )
    if(je == 0) {
        je = 1;
        Invoke("Timr", speed);
    }

    if(cas == 0) {
        //..load end in prikazi score
    }
   }
}