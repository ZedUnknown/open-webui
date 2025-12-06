<script>
	import { marked } from 'marked';
	import { replaceTokens, processResponseContent } from '$lib/utils';
	import { user } from '$lib/stores';

	import markedExtension from '$lib/utils/marked/extension';
	import markedKatexExtension from '$lib/utils/marked/katex-extension';
	import { disableSingleTilde } from '$lib/utils/marked/strikethrough-extension';
	import { mentionExtension } from '$lib/utils/marked/mention-extension';

	import MarkdownTokens from './Markdown/MarkdownTokens.svelte';
	import footnoteExtension from '$lib/utils/marked/footnote-extension';
	import citationExtension from '$lib/utils/marked/citation-extension';

	export let id = '';
	export let content;
	export let done = true;
	export let model = null;
	export let save = false;
	export let preview = false;

	export let editCodeBlock = true;
	export let topPadding = false;

	export let sourceIds = [];

	export let onSave = () => {};
	export let onUpdate = () => {};

	export let onPreview = () => {};

	export let onSourceClick = () => {};
	export let onTaskClick = () => {};

	let tokens = [];
	let contentBuffer = '';
	let bufferTimer = null;

	const options = {
		throwOnError: false,
		breaks: true
	};

	marked.use(markedKatexExtension(options));
	marked.use(markedExtension(options));
	marked.use(citationExtension(options));
	marked.use(footnoteExtension(options));
	marked.use(disableSingleTilde);
	marked.use({
		extensions: [mentionExtension({ triggerChar: '@' }), mentionExtension({ triggerChar: '#' })]
	});

	// clean up timer on component destroy
	import { onDestroy } from 'svelte';
	onDestroy(() => {
		if (bufferTimer) {
			clearTimeout(bufferTimer);
		}
	});

	// check if markdown content has unclosed syntax
	function hasUnclosedMarkdown(content) {
		// Check for unclosed ** (bold)
		const boldCount = (content.match(/\*\*/g) || []).length;
		if (boldCount % 2 !== 0) return true;
		
		// Check for unclosed * (italic)
		const italicCount = (content.match(/\*/g) || []).length;
		if (italicCount % 2 !== 0) return true;
		
		// Check for unclosed [] (links)
		const linkOpen = (content.match(/\[/g) || []).length;
		const linkClose = (content.match(/\]/g) || []).length;
		if (linkOpen > linkClose) return true;
		
		// Check for unclosed () (used in links)
		const parenOpen = (content.match(/\(/g) || []).length;
		const parenClose = (content.match(/\)/g) || []).length;
		if (parenOpen > parenClose) return true;
		
		// Check for unclosed ` (inline code)
		const inlineCodeCount = (content.match(/`/g) || []).length;
		if (inlineCodeCount % 2 !== 0) return true;
		
		// Check for unclosed ``` (code blocks)
		const codeBlockCount = (content.match(/```/g) || []).length;
		if (codeBlockCount % 2 !== 0) return true;
		
		return false;
	}

	$: {
		if (content !== undefined) {
			// completed content, process immediately
			if (done) {
				if (bufferTimer) {
					console.log('Clearing buffer timer at the end');
					clearTimeout(bufferTimer);
					bufferTimer = null;
				}
				
				try {
					const processedContent = replaceTokens(
						processResponseContent(content), 
						model?.name, 
						$user?.name
					);
					tokens = marked.lexer(processedContent);
				} catch (e) {
					console.error('Error processing markdown:', e);
					tokens = [];
				}
			} else {
				// streaming content, use adaptive buffering
				contentBuffer = content;
				
				if (bufferTimer) {
					console.log('Clearing buffer timer');
					clearTimeout(bufferTimer);
				}
				
				// buffer time based on markdown syntax completeness
				const bufferTime = hasUnclosedMarkdown(content) ? 200 : 20;
				
				bufferTimer = setTimeout(() => {
					try {
						const processedContent = replaceTokens(
							processResponseContent(contentBuffer), 
							model?.name, 
							$user?.name
						);
						tokens = marked.lexer(processedContent);
					} catch (e) {
						console.error('Error processing markdown:', e);
						tokens = [];
					}
				}, bufferTime);
			}
		} else {
			tokens = [];
		}
	}
</script>

{#key id}
	<MarkdownTokens
		{tokens}
		{id}
		{done}
		{save}
		{preview}
		{editCodeBlock}
		{sourceIds}
		{topPadding}
		{onTaskClick}
		{onSourceClick}
		{onSave}
		{onUpdate}
		{onPreview}
	/>
{/key}