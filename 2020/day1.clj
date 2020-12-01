(def stdin (java.io.BufferedReader. *in*))

(defn get-lines [r]
  (doall (map #(Integer/parseInt %) (line-seq r))))

(defn cartesian [colls]
  (if (empty? colls)
    '(())
    (for [more (cartesian (rest colls))
          x (first colls)]
      (cons x more))))

(let [lines (get-lines stdin)]
  (println
   (reduce * (first (filter (fn [line] (= (reduce + line) 2020))
                            (cartesian [lines lines])))))

  (println
   (reduce * (first (filter (fn [line] (= (reduce + line) 2020))
                            (cartesian [lines lines lines]))))))
