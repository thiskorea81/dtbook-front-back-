import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

export async function getPdfData(pdfDataUrl) {
  const pdf = await pdfjsLib.getDocument(pdfDataUrl).promise;
  const numPages = pdf.numPages;
  const pdfData = [];

  for (let i = 1; i <= numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const viewport = page.getViewport({ scale: 1 });

    const textItems = textContent.items.map(item => item.str);
    const text = textItems.join(' ');

    console.log(`Page ${i} Text:`, text);

    // 캔버스를 사용하여 페이지를 렌더링하고 이미지를 추출합니다.
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    await page.render({ canvasContext: context, viewport }).promise;
    const image = canvas.toDataURL();

    console.log(`Page ${i} Image:`, image);

    pdfData.push({ text, image, viewport });
  }

  return pdfData;
}
