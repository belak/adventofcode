(def stdin (java.io.BufferedReader. *in*))

(defn get-lines [r]
  (doall (map #(let [match (re-matches #"(\d+)-(\d+) (\w): (\w+)" %)]
                 [(Integer/parseInt (nth match 1))
                  (Integer/parseInt (nth match 2))
                  (first (nth match 3))
                  (nth match 4)])
              (line-seq r))))

(let [lines (get-lines stdin)]
  ;; Part 1
  (println
   (count
    (filter
     (fn [line]
       (let [letter-count (get (frequencies (nth line 3)) (nth line 2))]
         (and letter-count (<= (nth line 0) letter-count) (>= (nth line 1) letter-count))))
     lines)))

  ;; Part 2
  (println
   (count
    (filter
     (fn [line]
       (let [match1 (= (nth (nth line 3)
                            (- (nth line 0) 1))
                       (nth line 2))
             match2 (= (nth (nth line 3)
                            (- (nth line 1) 1))
                       (nth line 2))]

         (or (and match1 (not match2))
             (and match2 (not match1)))))

     lines))))
