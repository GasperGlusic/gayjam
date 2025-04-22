using UnityEngine;
using UnityEngine.SceneManagement;

public class  : MonoBehaviour
{
   int je = 0;
   public int cas;
   public float speed;

   void Timr() {
    cas--;
    je = 0;
   }

   void Update() {
    if(je == 0) {
        je = 1;
        Invoke("Timr", speed);
    }

    if(cas == 0) {
        //..load end in prikazi score
    }
   }
}