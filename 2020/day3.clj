(def stdin (java.io.BufferedReader. *in*))

(defn get-lines [r]
  (doall (line-seq r)))

(defn slope [lines & {:keys [dx dy] :or {dx 3 dy 1}}]
  (count
   (filter (fn [x] (= x \#))
           (map
            (fn [i]
              (let [x (* i dx)
                    y (* i dy)
                    line (nth lines y)]
                (nth line (rem x (count line)))))
            (range (quot (count lines) dy))))))

(let [lines (get-lines stdin)]
  ;; Part 1
  (println (slope lines))

  (println (*
            (slope lines :dx 1 :dy 1)
            (slope lines :dx 5 :dy 1)
            (slope lines :dx 7 :dy 1)
            (slope lines :dx 3 :dy 1)
            (slope lines :dx 1 :dy 2))))
