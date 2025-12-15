import React from 'react';
import clsx from 'clsx';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
  useWindowSize,
} from '@docusaurus/theme-common';
import {
  useDocsSidebar,
  useDocsSidebarCustomProps,
} from '@docusaurus/theme-common/internal';
import {useDocsVersion} from '@docusaurus/theme-common';
import DocPageLayoutSidebar from '@theme/DocPage/Layout/Sidebar';
import DocPageLayoutMain from '@theme/DocPage/Layout/Main';
import DocVersionBanner from '@theme/DocVersionBanner';
import styles from './LearningModuleLayout.module.css';

function LearningModuleLayout(props) {
  const {content: DocContent, versionMetadata} = props;
  const sidebar = useDocsSidebar();
  const {pluginId} = useDocsVersion();
  const sidebarPosition = useDocsSidebarCustomProps()?.sidebarPosition ?? 'left';
  const windowSize = useWindowSize();
  const hasSidebar = sidebar && (windowSize === 'desktop' || windowSize === 'ssr');

  return (
    <LayoutWrapper
      sidebarName={DocContent.metadata.sidebar}
      hasSidebar={hasSidebar}
      sidebarPosition={sidebarPosition}>
      <div className={styles.learningModuleContainer}>
        <div className={styles.learningModuleHeader}>
          <h1 className={styles.learningModuleTitle}>{DocContent.metadata.title}</h1>
          <div className={styles.learningModuleMetadata}>
            <span className={styles.learningModuleTime}>
              Reading time: {DocContent.metadata.readingTime} min
            </span>
            <span className={styles.learningModuleDifficulty}>
              Difficulty: {DocContent.metadata.frontMatter.difficulty || 'Intermediate'}
            </span>
          </div>
        </div>

        <div className={styles.learningModuleContent}>
          <DocVersionBanner versionMetadata={versionMetadata} />
          <DocContent />
        </div>

        <div className={styles.learningModuleFooter}>
          <div className={styles.learningModuleActions}>
            <button className={styles.actionButton}>
              <span className={styles.actionIcon}>←</span> Previous
            </button>
            <button className={styles.actionButton}>
              Next <span className={styles.actionIcon}>→</span>
            </button>
          </div>

          <div className={styles.learningModuleProgress}>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{width: '33%'}}></div>
            </div>
            <span className={styles.progressText}>Module Progress: 33%</span>
          </div>
        </div>
      </div>
    </LayoutWrapper>
  );
}

function LayoutWrapper({sidebarName, hasSidebar, sidebarPosition, children}) {
  const className = clsx(
    ThemeClassNames.page.docsDocPage,
    'row',
    'margin-top--lg',
    'margin-bottom--lg',
  );

  return (
    <HtmlClassNameProvider>
      <PageMetadata>
        <div className={className}>
          {hasSidebar && sidebarPosition === 'left' && (
            <div className="col col--3">
              <DocPageLayoutSidebar sidebarName={sidebarName} />
            </div>
          )}
          <div className={clsx('col', {'col--9': hasSidebar, 'col--12': !hasSidebar})}>
            {children}
          </div>
          {hasSidebar && sidebarPosition === 'right' && (
            <div className="col col--3">
              <DocPageLayoutSidebar sidebarName={sidebarName} />
            </div>
          )}
        </div>
      </PageMetadata>
    </HtmlClassNameProvider>
  );
}

export default LearningModuleLayout;