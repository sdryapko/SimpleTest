package diffprocessor;

import diffprocessor.SortedLimitedList.Entry;

/**
 * Created by VavilauA on 6/19/2015.
 */
public class Processor {
    private long l;
	public Processor(long limit) {
        l = limit;
    }

    @SuppressWarnings({ "unchecked", "rawtypes" })
	public void doProcess(SortedLimitedList<Double> mustBeEqualTo, SortedLimitedList<Double> expectedOutput) throws Exception {
        // TODO: make "mustBeEqualTo" list equal to "expectedOutput".
        // 0. Processor will be created once and then will be used billion times.
        // 1. Use methods: AddFirst, AddLast, AddBefore, AddAfter, Remove to modify list.
        // 2. Do not change expectedOutput list.
        // 3. At any time number of elements in list could not exceed the "Limit".
        // 4. "Limit" will be passed into Processor's constructor. All "mustBeEqualTo" and "expectedOutput" lists will have the same "Limit" value.
        // 5. At any time list elements must be in non-descending order.
        // 6. Implementation must perform minimal possible number of actions (AddFirst, AddLast, AddBefore, AddAfter, Remove).
        // 7. Implementation must be fast and do not allocate excess memory.
    	Entry uk1 = mustBeEqualTo.getFirst();
    	Entry uk2 = expectedOutput.getFirst();
    	if (mustBeEqualTo.getCount() > l || expectedOutput.getCount() > l) {
    		System.out.println("Bad Input");
    	}
    	/*
    	 * Тут всё плохо, так как уже не взазим в лимит.
    	 */
    	while (uk1 != null) {
    		while (uk2 != null && uk2.getValue().compareTo(uk1.getValue()) < 0) {
    			uk2 = uk2.getNext();
    		}
    		if (uk2 == null || uk2.getValue().equals(uk1.getValue()) == false) {
    			Entry tmp = uk1.getNext();
    			mustBeEqualTo.remove(uk1);
    			uk1 = tmp;
    		} else {
    			uk1 = uk1.getNext();
    			uk2 = uk2.getNext();
    		}
    	}
    	/*удаляем те, которых точно не будет, методом двух указателей. Это, очевидно, не нарушает отсортированности,
    	сложность этого O(n + m), где n и m - длины списков, так как каждый указатель не возвращается назад.
    	Мы не можем сразу добавлять и удалять, так как тогда мы бы могли вылезти за лимит, а так этого не сделаем, так как
    	вначале всё удаляем.
    	*/
    	uk1 = mustBeEqualTo.getFirst();
    	uk2 = expectedOutput.getFirst();
    	while (uk2 != null) {
    		while (uk1 != null && uk1.getValue().compareTo(uk2.getValue()) < 0) {
    			uk1 = uk1.getNext();
    		}

    		if (uk1 == null) {
    			mustBeEqualTo.addLast((Double) uk2.getValue());
    		} else if (uk1.getValue().equals(uk2.getValue())) {
    			uk1 = uk1.getNext();
    		} else {
    			mustBeEqualTo.addBefore(uk1, (Double) uk2.getValue());
    		}
    		uk2 = uk2.getNext();
    	}
    	/* Идея такая же, как и выше. Воспользуемся методом двух указателей для того, чтобы искать
    	 * позиции, куда вставлять. Очевидно, отсортированность не нарушается, так как мы выбираем
    	 * те позиции, куда стоит вставлять, чтобы она не нарушалась. Сложность O(n + m), как и в верхнем случае. 
    	 */
    }
}
