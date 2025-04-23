using UnityEngine;
using TMPro;

public class Detekcija : MonoBehaviour
{
   int i = 0;
   private Skore score;

   void Start() {
      score = GameObject.FindGameObjectWithTag("Skor").GetComponent<Skore>();
   }

   void OnTriggerStay2D(Collider2D other)
    {
       if(other.CompareTag("Player") && i == 0) {
         i = 1;
         score.score++;
         Destroy(gameObject, 1);
       }
    }
}