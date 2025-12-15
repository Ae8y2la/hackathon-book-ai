import React from 'react';
import clsx from 'clsx';
import styles from './ExerciseBox.module.css';

function ExerciseBox({title, difficulty, children, solution}) {
  const [showSolution, setShowSolution] = React.useState(false);

  return (
    <div className={styles.exerciseBox}>
      <div className={styles.exerciseHeader}>
        <h4 className={styles.exerciseTitle}>
          <span className={styles.exerciseIcon}>📝</span> {title}
        </h4>
        <span className={clsx(styles.difficulty, styles[difficulty.toLowerCase()])}>
          {difficulty}
        </span>
      </div>

      <div className={styles.exerciseContent}>
        {children}
      </div>

      {solution && (
        <div className={styles.exerciseFooter}>
          <button
            className={styles.solutionButton}
            onClick={() => setShowSolution(!showSolution)}
          >
            {showSolution ? 'Hide Solution' : 'Show Solution'}
          </button>

          {showSolution && (
            <div className={styles.solutionContent}>
              <h5>Solution:</h5>
              {solution}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ExerciseBox;